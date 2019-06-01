package dbops

import (
	db_defs "Project/flyjob/data_api/outdb/defs"

	web_defs "Project/flyjob/web/defs"
	"fmt"
	"gopkg.in/mgo.v2"
	"gopkg.in/mgo.v2/bson"
	"log"
)

var (
	session     *mgo_v2.Session
	KeyWordList []db_defs.Keys
	Queryapi    = bson.M{}
)

func init() {
	var err error
	session, err = mgo_v2.Dial(db_defs.MongoUrl)
	if err != nil {
		panic(err)
	}
	session.SetMode(mgo_v2.Monotonic, true)
}

// options := &defs.ReqBody{
// 		KeyWord: "C#",
// 		JobType: "",
// 		Limit:   20,
// 		Offset:  0,
// 	}
func GetJobsInfoList(options *web_defs.ReqBody) (*db_defs.ResultList, error) {
	s := session.Copy()
	defer s.Close()
	c := s.DB(db_defs.JobsInfoDB).C(fmt.Sprintf("%s%s", options.JobType, options.KeyWord))

	results := &db_defs.ResultList{}

	query := c.Find(nil)

	count, err := query.Count()
	if err != nil {
		log.Println(err)
		return nil, err
	}

	results.Count = count

	if err = query.Skip(options.Offset).Limit(options.Limit).All(&results.InfoList); err != nil {
		log.Println(err)
		return nil, err
	}
	return results, nil
}

// func GetKeyWord() ([]db_defs.Keys, error) {
// 	s := session.Copy()
// 	defer s.Close()
// 	c := s.DB(db_defs.KeyWordDB).C(db_defs.KeyWordCollction)
// 	err = c.Find(nil).All(&KeyWordList)
// 	if err != nil {
// 		log.Println(err)
// 		return nil, err
// 	}
// 	return KeyWordList, nil
// }

/*func GetJobsInfoList(ReqBody *webdefs.JobsRequestBody) (*defs.ResultList, error) {
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
}*/
