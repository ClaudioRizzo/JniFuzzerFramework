#include <stdio.h>
#include "function_ptrs.h"

double CallDouble(int n, void *fn, JNIEnv *env, jobject jobj, double *args) {
    if (n == 1) {
        auto ptr = (ExecDouble_1)fn;
        return ptr(env, jobj, args[0]);
    } else if (n == 2) {
        auto ptr = (ExecDouble_2)fn;
        return ptr(env, jobj, args[0], args[1]);
    } else {
        return NULL;
    }
}

void *call(int n, void *fn, JNIEnv *env, jobject jobj, void **args) {
    if (n == 0) {
        auto ptr = (ExecMePtr_0)fn;
        /* Do call */
        return ptr(env, jobj);
    }
    if (n == 1) {
        auto ptr = (ExecMePtr_1)fn;
        /* Do call */
        return ptr(env, jobj, args[0]);
    }
    if (n == 2) {
        auto ptr = (ExecMePtr_2)fn;
        /* Do call */
        return ptr(env, jobj, args[0], args[1]);
    }
    if (n == 3) {
        auto ptr = (ExecMePtr_3)fn;
        /* Do call */
        return ptr(env, jobj, args[0], args[1], args[2]);
    }
    if (n == 4) {
        auto ptr = (ExecMePtr_4)fn;
        /* Do call */
        return ptr(env, jobj, args[0], args[1], args[2], args[3]);
    }
    if (n == 5) {
        auto ptr = (ExecMePtr_5)fn;
        /* Do call */
        return ptr(env, jobj, args[0], args[1], args[2], args[3], args[4]);
    }

    return NULL;
}