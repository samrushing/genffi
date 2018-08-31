# -*- Mode: Makefile -*-

CC = clang
CFLAGS = -I. -O3 -fomit-frame-pointer
INCS = irken.h rdtsc.h gc1.c header1.c
OBJS = genffi.o
SRCS = genffi.c

all: genffi

genffi.o: $(INCS)

genffi: $(OBJS)
