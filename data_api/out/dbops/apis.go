package dbops

import (
	"Project/flyjob/data_api/out/defs"

	"gopkg.in/mgo.v2"
	"gopkg.in/mgo.v2/bson"
	"log"
)

var (
	session *mgo_v2.Session
)

func init() {
	var err error
	session, err = mgo_v2.Dial(defs.MongoUrl)
	if err != nil {
		panic(err)
	}
	session.SetMode(mgo_v2.Monotonic, true)
}

func GetJobsInfoList(ReqBody *defs.JobsRequestBody) (*defs.ResultList, error) {

	var results defs.ResultList
	s := session.Copy()
	defer s.Close()
	//defer session.Close()
	//log.Println(ReqBody.Salary,ReqBody.City)
	c := s.DB(defs.JobsInfoDB).C(ReqBody.JobType + ReqBody.Keyword)
	err := c.Find(bson.M{"salary": ReqBody.Salary, "city": ReqBody.City}).All(&results.JobsInfoList)
	//log.Println(results.JobsInfoList,c.Name,)
	if err != nil {
		log.Println(err)
		return nil, err
	}
	results.JobsCount = len(results.JobsInfoList)
	return &results, nil
}
