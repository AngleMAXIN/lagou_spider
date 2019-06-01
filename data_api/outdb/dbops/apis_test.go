package dbops

import (
	"Project/flyjob/web/defs"
	"encoding/json"
	"fmt"
	"testing"
)

func TestMain(m *testing.M) {
	m.Run()
}

func TestGetJobsInfoList(t *testing.T) {

	options := &defs.ReqBody{
		KeyWord: "Java",
		JobType: "fw",
		Limit:   20,
		Offset:  10,
	}
	res, err := GetJobsInfoList(options)

	if err != nil {
		t.Error(err)
	}
	data, err := json.MarshalIndent(res, " ", " ")
	if err != nil {
		return
	}
	fmt.Printf("%s", data)
}
