package main

import (
	"fmt"
	"gopkg.in/mgo.v2"
	"gopkg.in/mgo.v2/bson"
)

var (
	session     *mgo_v2.Session
	InfoDBName  string = "jobs_info"
	LimitDBName string = "jobs_limit"
)

type JobInfo struct {
	//_Id          string
	JobName     string
	Salary      string
	WorkYear    string
	Education   string
	CompanyName string
	CompanySize string
	CompanyType string
	CompanyLogo string
	CompanyUrl  string
	PositionUrl string
}

func FindResult(collection, city, salay string) []JobInfo {
	var result []JobInfo
	c := session.DB(InfoDBName).C(collection)

	err := c.Find(bson.M{"salary": salay, "city": city}).All(&result)
	if err != nil {
		panic(err)
	}
	return result
}

func main() {
	session, err := mgo_v2.Dial("127.0.0.1:27017")
	if err != nil {
		panic(err)
	}
	session.SetMode(mgo_v2.Monotonic, true)

	defer session.Close()
	collection := "python"
	city := "上海"
	salay := "10k-15k"
	r := FindResult(collection, city, salay)
	for i, v := range r {
		fmt.Println(i, v)
	}

}
