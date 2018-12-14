package main

import (
	"net/http"
	"github.com/julienschmidt/httprouter"
)

func RegisterHandlers() *httprouter.Router {
	router := httprouter.New()

	router.POST("/api_v1/joblist",GetJobsInfo)

	return router
}

func main() {
	//	Prepare()
	// 注册路由
	r := RegisterHandlers()
	http.ListenAndServe(":8080", r)

}