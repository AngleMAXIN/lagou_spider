package main

import (
	"Project/flyjob/data_api/out/dbops"
	//"Project/flyjob/data_api/out/defs"
	"Project/flyjob/web/defs"
	"encoding/json"
	"github.com/julienschmidt/httprouter"
	"html/template"
	"io/ioutil"
	"log"
	"strconv"
	"net/http"
)

type ChoiceList struct {
	KeyWord []string
	City    []string
	Salary  []string
	EleType []string
}

func HomeHandler(w http.ResponseWriter, r *http.Request, p httprouter.Params) {
	var data = ChoiceList{}

	keyWordList, err := dbops.GetKeyWord()
	if err != nil {
		log.Println(err)
		SendErrorResponse(w, defs.ErrorDBError)
		return
	}
	for _, k := range keyWordList {
		data.KeyWord = append(data.KeyWord, k.KeyWord)
	}
	t := template.Must(template.ParseFiles("../templates/index.html"))
	if err != nil {
		log.Println(err)
	}

	t.Execute(w, data)
	return

}
func GetJobsInfoHandler(w http.ResponseWriter, r *http.Request, p httprouter.Params) {
	page,err := strconv.Atoi(p.ByName("page"))
	if err != nil {
		SendErrorResponse(w, defs.ErrorRequestBodyParseFailed)
		return
	}
	res, _ := ioutil.ReadAll(r.Body)

	// 解析json数据到结构体，出错则返回
	ubody := &defs.JobsRequestBody{}
	if err := json.Unmarshal(res, ubody); err != nil {
		SendErrorResponse(w, defs.ErrorRequestBodyParseFailed)
		return
	}

	// 根据请求数据创建用户，出错则返回
	results, err := dbops.GetJobsInfoList(ubody,page)
	if err != nil {
		SendErrorResponse(w, defs.ErrorDBError)
		return
	}

	w.Header().Set("Access-Control-Allow-Origin", "*")
	w.Header().Add("Access-Control-Allow-Headers", "Content-Type") // header的类型
	w.Header().Set("content-type", "application/json")

	Response, err := json.Marshal(results)
	if err != nil {
		SendErrorResponse(w, defs.ErrorInternalFaults)
	} else {
		SendNormalResponse(w, string(Response), 200)
	}

}
