CC = gcc
CFLAGS = -Wall -Wextra -g

SDL2 = `pkg-config --libs --cflags sdl2 SDL2_ttf`

TARGET = dungeon
OBJECTS = main.o map.o tile.o

.PHONY: all clean
all: $(TARGET)

$(TARGET): $(OBJECTS)
	$(CC) $(CFLAGS) $(SDL2) $^ -o $@

%.o: %.c
	$(CC) $(CFLAGS) $^ -c

run: $(TARGET)
	./$<

clean:
	@rm -fv $(TARGET) *.o