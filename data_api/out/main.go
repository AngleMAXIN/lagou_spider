package main

import (
	"fmt"
	"github.com/julienschmidt/httprouter"
	"net/http"
)

func RegisterHandlers() *httprouter.Router {
	router := httprouter.New()

	router.POST("/api_v1/jobs", GetJobsInfo)

	return router
}

func main() {
	//	Prepare()
	// 注册路由
	fmt.Println("listen on 8080")
	r := RegisterHandlers()
	http.ListenAndServe(":8080", r)

}
