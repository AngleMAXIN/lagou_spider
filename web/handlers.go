package main

import (
	"Project/flyjob/data_api/out/dbops"
	"Project/flyjob/data_api/out/defs"
	"encoding/json"
	"github.com/julienschmidt/httprouter"
	"io/ioutil"
	"net/http"
	"log"
	"html/template"
	defs2 "Project/flyjob/web/defs"
)

type ChoiceList struct {
	KeyWord []string
	//City []string
	//Salary []string
	//EleType []string
}

func HomeHandler(w http.ResponseWriter, r *http.Request, p httprouter.Params){
	var data = ChoiceList{}
	keyWordList, err := dbops.GetKeyWord()
	if err != nil{
		log.Println(err)
		SendErrorResponse(w,defs.ErrorDBError)
		return
	}
	for _,k := range keyWordList {
		data.KeyWord = append(data.KeyWord,k.KeyWord)
	}

	t,err := template.ParseFiles("./templates/index.html")
	//t.Parse(`{{.}}1)
	if err != nil {
		log.Println(err)
	}

	t.Execute(w,data)
	return

}
func GetJobsInfoHandler(w http.ResponseWriter, r *http.Request, p httprouter.Params) {

	res, _ := ioutil.ReadAll(r.Body)

	// 解析json数据到结构体，出错则返回

	ubody := &defs2.JobsRequestBody{}
	if err := json.Unmarshal(res, ubody); err != nil {
		SendErrorResponse(w, defs.ErrorRequestBodyParseFailed)
		return
	}

	// log.Println(string(res),ubody)
	// 根据请求数据创建用户，出错则返回
	results, err := dbops.GetJobsInfoList(ubody)
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
