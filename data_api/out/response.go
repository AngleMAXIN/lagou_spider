package main

import (
	"Project/flyjob/data_api/out/defs"
	"encoding/json"
	"io"
	"net/http"
)

func SendErrorResponse(w http.ResponseWriter, errResp defs.ErrorResponse) {

	w.WriteHeader(errResp.HttpSC)
	//w.Header().Set("Access-Control-Allow-Origin", "*")

	resStr, _ := json.Marshal(&errResp.Error)
	io.WriteString(w, string(resStr))

}

func SendNormalResponse(w http.ResponseWriter, resp string, sc int) {
	w.WriteHeader(sc)
	io.WriteString(w, resp)
}
