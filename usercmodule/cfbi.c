// Include MicroPython API.

#include "py/runtime.h"

// This is the function which will be called from Python  -------------------------------------------
// rotate coordinate px py clockwise around  other coordinate ox oy (px,py,deg,ox,oy)

#include <math.h>

// M_PI is not part of the math.h standard and may not be defined
// And by defining our own we can ensure it uses the correct const format.

#define MP_PI MICROPY_FLOAT_CONST(3.14159265358979323846)

#define degToRad(angleInDegrees) ((angleInDegrees) * M_PI / 180.0)
#define radToDeg(angleInRadians) ((angleInRadians) * 180.0 / M_PI)

static mp_obj_t cfbi_rotatexy(size_t n_args, const mp_obj_t *args) {

        mp_float_t px  = 0.0;
        mp_float_t py  = 0.0; 
        mp_float_t deg = 0.0;
        mp_float_t ox  = 0.0;
        mp_float_t oy  = 0.0;

        if (mp_obj_is_float(args[0]))
          { px = mp_obj_float_get(args[0]); }
        else if (mp_obj_is_int(args[0]))
          { px = (mp_float_t)mp_obj_get_int(args[0]); }
        else
          { mp_raise_TypeError(MP_ERROR_TEXT("argument[0] not int or float !"));
            return mp_const_none; }

        if (mp_obj_is_float(args[1]))
          { py = mp_obj_float_get(args[1]); }
        else if (mp_obj_is_int(args[1]))
          { py = (mp_float_t)mp_obj_get_int(args[1]); }
        else
          { mp_raise_TypeError(MP_ERROR_TEXT("argument[1] not int or float !"));
            return mp_const_none; }

        if (mp_obj_is_float(args[2]))
          { deg = mp_obj_float_get(args[2]); }
        else if (mp_obj_is_int(args[2]))
          { deg = (mp_float_t)mp_obj_get_int(args[2]); }
        else
          { mp_raise_TypeError(MP_ERROR_TEXT("argument[2] not int or float !"));
            return mp_const_none; }

        if (mp_obj_is_float(args[3]))
          { ox = mp_obj_float_get(args[3]); }
        else if (mp_obj_is_int(args[3]))
          { ox = (mp_float_t)mp_obj_get_int(args[3]); }
        else
          { mp_raise_TypeError(MP_ERROR_TEXT("argument[3] not int or float !"));
            return mp_const_none; }

        if (mp_obj_is_float(args[4]))
          { oy = mp_obj_float_get(args[4]); }
        else if (mp_obj_is_int(args[4]))
          { oy = (mp_float_t)mp_obj_get_int(args[4]); }
        else
          { mp_raise_TypeError(MP_ERROR_TEXT("argument[4] not int or float !"));
            return mp_const_none; }

        mp_float_t x=px-ox;
        mp_float_t y=oy-py;

        mp_float_t r  = MICROPY_FLOAT_C_FUN(sqrt)(powf(x,2)+powf(y,2));

        mp_float_t rad = MICROPY_FLOAT_C_FUN(atan2)(y,x);

        mp_float_t degreexy=radToDeg(rad);

        if (degreexy < 0.0) {degreexy=360.0+degreexy;}

        deg=deg+degreexy;

        rad=degToRad(deg); 

        mp_float_t c = MICROPY_FLOAT_C_FUN(cos)(rad);
        mp_float_t s = MICROPY_FLOAT_C_FUN(sin)(rad);

        mp_float_t ret_x = ox+r*c;
        mp_float_t ret_y = oy+-(r*s);
  
        mp_obj_t tuple[2]={mp_obj_new_float(ret_x),mp_obj_new_float(ret_y)};

        return mp_obj_new_tuple(2, tuple);
    }

// Define a Python reference to the function above.
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(cfbi_rotatexy_obj,5,5,cfbi_rotatexy);

// This is the class ch which will be called from Python -------------------------------------------------

#include "extmod/font_petme128_8x8.h"

// This structure represents ch instance objects.

typedef struct _cfbi_ch_obj_t {
    // All objects start with the base.
    mp_obj_base_t base;
    // Everything below can be thought of as instance attributes, but they
    // cannot be accessed by MicroPython code directly. In this example we
    // store the time at which the object was created.
    int16_t i; // index for a character in  font_petme128_8x8
} cfbi_ch_obj_t;

const mp_obj_type_t cfbi_ch_type;

// This represents ch.__new__ and ch.__init__, which is called when the user instantiates a ch object. 

static mp_obj_t cfbi_ch_make_new (const mp_obj_type_t *type, size_t n_args, size_t n_kw, const mp_obj_t *args) {
       mp_arg_check_num(n_args, n_kw, 1, 1, true);
       cfbi_ch_obj_t *self = mp_obj_malloc(cfbi_ch_obj_t, type); // Allocates the new object and sets the type.
       size_t len;
       const byte *str = (const byte *)mp_obj_str_get_data(args[0], &len); // pointer to parameter character string
       if (len == 1) {
         uint8_t cnr = *(uint8_t *)str; // convert to int order number
         if (cnr < 32 || cnr > 127) // test cnr is in range
            { cnr = 32;}            // if cnr not in range set order nummer to 32 (character ' ')
         self->i =(cnr - 32)<<3;   // set index i to cnr character stored in 8 byte in from internal font "extmod/font_petme128_8x8.h"
       }
       else {mp_raise_TypeError(MP_ERROR_TEXT("Invalid ascii character"));}
       return MP_OBJ_FROM_PTR(self);
};


// This is the ch.pixel(x,y) method. After creating a ch object, this
// return true if bit is set in character stored in 8 byte in from internal font "extmod/font_petme128_8x8.h"
//        else false

static mp_obj_t cfbi_ch_pixel (mp_obj_t self_in, mp_obj_t x_in, mp_obj_t y_in) {
       
       cfbi_ch_obj_t *self = MP_OBJ_TO_PTR(self_in);

       mp_int_t x=mp_obj_get_int(x_in);
       mp_int_t y=mp_obj_get_int(y_in);

       if ( x<0 || x>7 || y<0 || y>7) {return mp_obj_new_bool(0);}

       const uint8_t *chr_data = &font_petme128_8x8[self->i];

       if (chr_data[x]&(1<<y)) 
         {return mp_obj_new_int(1);}
       else
         {return mp_obj_new_int(0);}

};

static MP_DEFINE_CONST_FUN_OBJ_3(cfbi_ch_pixel_obj, cfbi_ch_pixel);

// This collects all methods and other static class attributes of the ch.
// The table structure is similar to the module table, as detailed below.

static const mp_rom_map_elem_t cfbi_ch_locals_dict_table[] = {
{ MP_ROM_QSTR(MP_QSTR_pixel), MP_ROM_PTR(&cfbi_ch_pixel_obj) },
};

static MP_DEFINE_CONST_DICT(cfbi_ch_locals_dict, cfbi_ch_locals_dict_table);

// This defines the type(ch) object.

MP_DEFINE_CONST_OBJ_TYPE(
    cfbi_type_ch,
    MP_QSTR_ch,
    MP_TYPE_FLAG_NONE,
    make_new, cfbi_ch_make_new,
    locals_dict, &cfbi_ch_locals_dict
    );

// Define all attributes of the module.
// Table entries are key/value pairs of the attribute name (a string)
// and the MicroPython object reference.
// All identifiers and strings are written as MP_QSTR_xxx and will be
// optimized to word-sized integers by the build system (interned strings).

static const mp_rom_map_elem_t cfbi_module_globals_table[] = {
    // module name
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_cfbi) },
    { MP_ROM_QSTR(MP_QSTR_rotatexy), MP_ROM_PTR(&cfbi_rotatexy_obj) },
    { MP_ROM_QSTR(MP_QSTR_ch),      MP_ROM_PTR(&cfbi_type_ch) },
};
   
static MP_DEFINE_CONST_DICT(cfbi_module_globals,cfbi_module_globals_table);

// Define module object.

const mp_obj_module_t cfbi_module = {
    .base = { &mp_type_module },
    .globals = (mp_obj_dict_t*)&cfbi_module_globals,
};

// Register the module to make it available in Python

MP_REGISTER_MODULE(MP_QSTR_cfbi, cfbi_module);
