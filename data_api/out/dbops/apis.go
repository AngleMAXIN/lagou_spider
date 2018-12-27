package dbops

import (
	"Project/flyjob/data_api/out/defs"

	defs2 "Project/flyjob/web/defs"
	"gopkg.in/mgo.v2"
	"gopkg.in/mgo.v2/bson"
	"log"
)

var (
	session     *mgo_v2.Session
	KeyWordList []defs.Keys
	results     defs.ResultList
	err         error
	Queryapi    = bson.M{}
)

func init() {
	var err error
	session, err = mgo_v2.Dial(defs.MongoUrl)
	if err != nil {
		panic(err)
	}
	session.SetMode(mgo_v2.Monotonic, true)
}

func GetKeyWord() ([]defs.Keys, error) {
	s := session.Copy()
	defer s.Close()
	c := s.DB(defs.KeyWordDB).C(defs.KeyWordCollction)
	err = c.Find(nil).All(&KeyWordList)
	if err != nil {
		log.Println(err)
		return nil, err
	}
	return KeyWordList, nil
}

func GetJobsInfoList(ReqBody *defs2.JobsRequestBody) (*defs.ResultList, error) {
	s := session.Copy()
	defer s.Close()

	c := s.DB(defs.JobsInfoDB).C(ReqBody.JobType + ReqBody.Keyword)

	if ReqBody.City == "不限" {
		Queryapi["city"] = bson.M{"$exists": 1}
	} else {
		Queryapi["city"] = ReqBody.City

	}
	if len(ReqBody.Salary) == 0 {
		Queryapi["salary"] = bson.M{"$exists": 1}

	} else {
		//  ReqBody.Salary[0] <= salary < ReqBody.Salary[1]
		Queryapi["tag"] = bson.M{"$gte": ReqBody.Salary[0], "$lt": ReqBody.Salary[1]}
	}
	log.Println("Query:",Queryapi)
	err = c.Find(Queryapi).Limit(9).All(&results.JobsInfoList)

	if err != nil {
		log.Println(err)
		return nil, err
	}
	results.JobsCount = len(results.JobsInfoList)
	return &results, nil
}
