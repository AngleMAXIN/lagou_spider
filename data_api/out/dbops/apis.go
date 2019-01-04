package dbops

import (
	"Project/flyjob/data_api/out/defs"

	webdefs "Project/flyjob/web/defs"
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

func GetJobsInfoList(ReqBody *webdefs.JobsRequestBody) (*defs.ResultList, error) {
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
		Queryapi["tag"] = bson.M{"$gte": ReqBody.Salary[0], "$lt": ReqBody.Salary[1]}
	}
	log.Println("Query:", Queryapi)
	QueryResult := c.Find(Queryapi)
	results.JobsCount, err = QueryResult.Count()
	if err != nil {
		log.Println(err)
	}
	QueryResult.Skip(0 * 9).Limit(9).Sort("_id").All(&results.JobsInfoList)

	if err != nil {
		log.Println(err)
		return nil, err
	}
	return &results, nil
}
