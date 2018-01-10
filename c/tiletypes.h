#ifndef TILETYPES_H_
#define TILETYPES_H_

extern const char * imagefiles16[];
extern const char * imagefiles32[];
extern const char * tiledesc[];
/*  Indexes an array of SDL_Texture *
*/
typedef enum {
    DEFAULT = 0,
    WHITE,
    RED,
    GREEN,
    BLUE,
    ATT,
    FLOOR,
    B_TOPLEFT,
    B_TOPRIGHT,
    B_BOTTOMLEFT,
    B_BOTTOMRIGHT,
    B_HORIZONTAL,
    B_VERTICAL,
    // Used as a dynamic tally on the number of types.
    TILENUM 
} tiletype_t;

#endif /* TILETYPES_H_ */