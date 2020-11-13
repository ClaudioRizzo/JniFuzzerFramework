#ifndef _FUNCTION_PTRS_H
#define _FUNCTION_PTRS_H
#include <jni.h>

// NARGS 5

typedef void *(*ExecMePtr_0)(JNIEnv *, jobject);
typedef void *(*ExecMePtr_1)(JNIEnv *, jobject, void *);
typedef void *(*ExecMePtr_2)(JNIEnv *, jobject, void *, void *);
typedef void *(*ExecMePtr_3)(JNIEnv *, jobject, void *, void *, void *);
typedef void *(*ExecMePtr_4)(JNIEnv *, jobject, void *, void *, void *, void *);
typedef void *(*ExecMePtr_5)(JNIEnv *, jobject, void *, void *, void *, void *,
                             void *);

typedef double (*ExecDouble_1)(JNIEnv *, jobject, double);
typedef double (*ExecDouble_2)(JNIEnv *, jobject, double, double);
/**
 * This function is used to executed the function pointer `fn` given the
 * arguments `args`.
 * fn has to be a function extract from a shared library with the
 * extractor in this project. In other word, has to be a user defined
 * jni function.
 *
 * Params:
 *      int n:        number of parameters
 *      void* fn:     function to be call
 *      JNIEnv *evn:  An environment to pass to the function call
 *      jobject jobj: jobject to pass to the function call
 *      void** args:  arguments for the function call
 *
 * Return:
 *      void* : the result of calling `fn` with `args`
 */
void *call(int n, void *fn, JNIEnv *env, jobject jobj, void **args);
double CallDouble(int n, void* fn, JNIEnv *env, jobject jobj, double *args);
#endif
