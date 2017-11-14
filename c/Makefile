CC = gcc
CFLAGS := -Wall -Wextra -g
CFLAGS += $(shell pkg-config sdl2 SDL2_ttf SDL2_image --cflags)

LFLAGS = $(shell pkg-config sdl2 SDL2_ttf SDL2_image --libs)

TARGET = dungeon
OBJECTS = main.o map.o tile.o images.o list.o msg_module.o
HEADERS = map.h tile.h tiletypes.h list.h msg_module.h

.PHONY: all clean
all: $(TARGET)

$(TARGET): $(OBJECTS)
	$(CC) $^ -o $@ $(LFLAGS)

%.o: %.c $(HEADERS) 
	$(CC) $(CFLAGS) $< -c

run: $(TARGET)
	./$<

clean:
	@rm -fv $(TARGET) *.o