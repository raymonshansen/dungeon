CC = gcc
CFLAGS = -Wall -Wextra -g

SDL2 = `pkg-config --libs --cflags sdl2 SDL2_ttf SDL2_image`

TARGET = dungeon
OBJECTS = main.o map.o tile.o images.o
HEADERS = map.h tile.h tiletypes.h

.PHONY: all clean
all: $(TARGET)

$(TARGET): $(OBJECTS)
	$(CC) $(CFLAGS) $(SDL2) $^ -o $@

%.o: %.c $(HEADERS) 
	$(CC) $(CFLAGS) $< -c

run: $(TARGET)
	./$<

clean:
	@rm -fv $(TARGET) *.o