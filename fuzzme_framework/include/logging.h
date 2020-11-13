#ifndef _LOGGING_H
#define _LOGGING_H

#include <stdio.h>
#include <stdlib.h>
#include <string>

#ifdef DEBUG
#define LOG_DEBUG(f_, ...)     \
    printf("[debug] ");        \
    printf(f_, ##__VA_ARGS__); \
    printf("\n");

#define LOG_FILE_DEBUG(f_, ...)             \
    {                                       \
        FILE *fd = fopen("debug.log", "a"); \
        fprintf(fd, f_, ##__VA_ARGS__);     \
        fprintf(fd, "\n");                  \
        fclose(fd);                         \
    }

#else
#define LOG_DEBUG(f_, ...)
#endif

#define LOG(tag, f_, ...)      \
    printf("[%s]", tag);       \
    printf(f_, ##__VA_ARGS__); \
    printf("\n");
#define LOG_INFO(f_, ...)      \
    printf("[info] ");         \
    printf(f_, ##__VA_ARGS__); \
    printf("\n");

#ifdef VERBOSE
#define LOG_ERR(f_, ...)                \
    fprintf(stderr, "[err] ");          \
    fprintf(stderr, f_, ##__VA_ARGS__); \
    fprintf(stderr, "\n");
#define LOG_WARNING(f_, ...)   \
    printf("[warning] ");      \
    printf(f_, ##__VA_ARGS__); \
    printf("\n");
#else
#define LOG_ERR(f_, ...)
#define LOG_WARNING(f_, ...)
#endif

#endif