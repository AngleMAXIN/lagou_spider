package main

import (
	"net/http"
	"github.com/julienschmidt/httprouter"
	"Project/video_server/api/defs"
	"encoding/json"
	"Project/video_server/api/dbops"
	"io/ioutil"
)

func GetJobsInfo(w http.ResponseWriter, r *http.Request, p httprouter.Params)  {
	es, _ := ioutil.ReadAll(r.Body)

	//解析json数据到结构体，出错则返回
	ubody := &defs.UserCredential{}
	if err := json.Unmarshal(res, ubody); err != nil {
		SendErrorResponse(w, defs.ErrorRequestBodyParseFailed)
		return
	}

	//根据请求数据创建用户，出错则返回
	if err := dbops.AddUserCredential(ubody.Username, ubody.Pwd); err != nil {
		SendErrorResponse(w, defs.ErrorDBError)
		return
	}
}