package main

import (
	"Project/flyjob/data_api/out/dbops"
	"Project/flyjob/data_api/out/defs"
	"encoding/json"
	"github.com/julienschmidt/httprouter"
	"io/ioutil"
	"net/http"
	)

func GetJobsInfo(w http.ResponseWriter, r *http.Request, p httprouter.Params) {

	res, _ := ioutil.ReadAll(r.Body)

	//解析json数据到结构体，出错则返回

	ubody := &defs.JobsRequestBody{}
	if err := json.Unmarshal(res, ubody); err != nil {
		SendErrorResponse(w, defs.ErrorRequestBodyParseFailed)
		return
	}

	//log.Println(string(res),ubody)
	//根据请求数据创建用户，出错则返回
	results, err := dbops.GetJobsInfoList(ubody)
	if err != nil {
		SendErrorResponse(w, defs.ErrorDBError)
		return
	}
	w.Header().Set("Access-Control-Allow-Origin", "*")
	w.Header().Add("Access-Control-Allow-Headers", "Content-Type") //header的类型
	w.Header().Set("content-type", "application/json")
	Response, err := json.Marshal(results)
	if err != nil {
		SendErrorResponse(w, defs.ErrorInternalFaults)
	} else {
		SendNormalResponse(w, string(Response), 200)
	}

}
