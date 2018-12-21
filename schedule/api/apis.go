package main

import (
	"Project/flyjob/data_api/out/defs"
	"fmt"
	"gopkg.in/mgo.v2"
	"gopkg.in/mgo.v2/bson"
	"log"
	"regexp"
	"strconv"
)

type JobInfo struct {
	Salary string `json:"salary"`
	_Id    string `json:"id"`
}

var (
	session   *mgo_v2.Session
	salaryRe  = regexp.MustCompile(`([0-9]+)K-([0-9]+)K`)
	ChangeKey []JobInfo
)

func init() {
	var err error
	session, err = mgo_v2.Dial(defs.MongoUrl)
	if err != nil {
		panic(err)
	}
	session.SetMode(mgo_v2.Monotonic, true)
}

func getAllCollections() []string {
	s := session.Copy()
	defer s.Close()
	c1, _ := s.DB(defs.JobsInfoDB).CollectionNames()

	return c1
}

func GetJobsInfoList(CollName string) (*[]JobInfo, error) {

	//var results defs.ResultList
	s := session.Copy()
	defer s.Close()

	c := s.DB(defs.JobsInfoDB).C(CollName)
	err := c.Find(bson.M{"salary": bson.M{"$exists": 1}}).All(&ChangeKey)
	// fmt.Println(c, ChangeKey)
	if err != nil {
		log.Println(err)
		return nil, err
	}
	//results.JobsCount = len(ChangeKey)
	return &ChangeKey, nil
}

func task(datalist *[]JobInfo) {
	var start int
	var end int
	var err error
	for _, data := range *datalist {
		all := salaryRe.FindAllSubmatch([]byte(data.Salary), -1)
		for _, m := range all {
			// fmt.Println(string(m))
			start,err = strconv.Atoi(string(m[1]))
			if err != nil {
				log.Println(err)
			}
			end, err = strconv.Atoi(string(m[2]))
			if err != nil {
				log.Println(err)
			}
			fmt.Printf("%sK - %sK ---> %d\n",string(m[1]),string(m[2]),(end + start) / 2)
		}
	}
}

func main() {
	collections := getAllCollections()
	for _, coll := range collections[:2] {
		resultList, e := GetJobsInfoList(coll)
		// fmt.Println(resultList)
		if e != nil {
			log.Println(e)
		}
		// fmt.Println("----")
		task(resultList)
	}

}
