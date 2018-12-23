package main

import (
		"github.com/julienschmidt/httprouter"
	"net/http"
)

func RegisterHandlers() *httprouter.Router {
	router := httprouter.New()

	router.GET("/",HomeHandler)
	router.POST("/api_v1/jobs", GetJobsInfoHandler)

	router.ServeFiles("/statics/*filepath",http.Dir("./templates"))
	return router
}

func main() {
	//	Prepare()
	// 注册路由
	//fmt.Println("listen on 8080fef")
	r := RegisterHandlers()
	http.ListenAndServe(":8080", r)

}
