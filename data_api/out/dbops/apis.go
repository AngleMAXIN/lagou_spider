package dbops

import (
	_ "encoding/json"
	"fmt"
	"gopkg.in/mgo.v2"
	"gopkg.in/mgo.v2/bson"
	"Project/websocket/defs"
)

var (
	session *mgo_v2.Session
)

func init() {
	session, err := mgo_v2.Dial(defs.MongoUrl)
	if err != nil {
		panic(err)
	}
	session.SetMode(mgo_v2.Monotonic, true)
}

func GetJobsInfoList(collection, city, salary string) defs.ResultList {
	var results defs.ResultList

	defer session.Close()
	c := session.DB(defs.JobsInfoDB).C(collection)

	err := c.Find(bson.M{"salary": salary, "city": city}).All(&results.JobsInfoList)
	if err != nil {
		fmt.Println(err)
	}
	results.JobsCount = len(results.JobsInfoList)
	return results
}
