NUM_ARGS=$(($1))

echo "#ifndef _FUNCTION_PTRS_H"
echo "#define _FUNCTION_PTRS_H"
echo "#include <jni.h>"
echo ""
echo "//NARGS ${NUM_ARGS}"
echo ""
for i in $(seq 0 $NUM_ARGS) 
do
  printf "typedef void * (*ExecMePtr_$i) (JNIEnv *, jobject"
  for j in $(seq 1 $i)
  do
    printf ",void*"
  done
  printf ");\n"
done

printf "void call(int n, void* fn, JNIEnv *env, jobject jobj, void **args) {\n\n"

for i in $(seq 0 $NUM_ARGS)
do
  printf "if (n == $i) {\n"
  printf "auto ptr = (ExecMePtr_$i) fn;\n"
  printf "/* Do call */\n";
  printf "return ptr(env, jobj"
  for j in $(seq 0 $(($i-1)))
  do
    printf ", args[$j]"
  done
  printf ");\n}\n"
done
printf "return NUL;\n"
printf "}\n"

echo "#endif"