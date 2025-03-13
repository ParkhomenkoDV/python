package main

import "C"

//export DoSmth
func DoSmth() {
	println("Hello from Golang!")
}

//export get_some_num
func get_some_num() int8 {
	return 32
}

//export Add
func Add(a, b int) int {
	return a + b
}

func main() {}

//go mod init lib

//скомпилировать библиотеку в терминале
//go build -buildmode=c-shared lib.go

//дописать расширение dll

//в Python:
//import ctypes
//lib = ctypes.CDLL("./lib.dll")
//lib.do_smth()
//num = lib.get_some_num()
