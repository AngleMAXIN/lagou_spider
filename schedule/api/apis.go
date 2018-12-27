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
	Salary string        `json:"salary"`
	Id     bson.ObjectId `bson:"_id"`
}

var (
	session   *mgo_v2.Session
	salaryRe  = regexp.MustCompile(`([0-9]+)[k|K]-([0-9]+)[k|K]`)
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

func GetJobsInfoList(CollName string, field string, exist int) (*[]JobInfo, error) {

	//var results defs.ResultList
	s := session.Copy()
	defer s.Close()

	c := s.DB(defs.JobsInfoDB).C(CollName)
	err := c.Find(bson.M{field: bson.M{"$exists": exist}}).All(&ChangeKey)
	if err != nil {
		log.Println(err)
		return nil, err
	}
	return &ChangeKey, nil
}

func AddComLogoTask(datalist *[]JobInfo, coll string) {
	s := session.Copy()
	defer s.Close()

	c := s.DB(defs.JobsInfoDB).C(coll)

}

func AddTagTask(datalist *[]JobInfo, coll string) {
	var (
		start  int
		end    int
		err    error
		updata = bson.M{}
	)

	s := session.Copy()
	defer s.Close()

	c := s.DB(defs.JobsInfoDB).C(coll)

	for _, data := range *datalist {
		selector := bson.M{"_id": data.Id}

		if data.Salary == "薪资面议" || data.Salary == "校招" {
			updata = bson.M{"$set": bson.M{"tag": 0}}
		} else {

			all := salaryRe.FindAllSubmatch([]byte(data.Salary), -1)

			for _, m := range all {

				start, err = strconv.Atoi(string(m[1]))
				if err != nil {
					log.Println(err)
				}
				end, err = strconv.Atoi(string(m[2]))
				if err != nil {
					log.Println(err)
				}
				updata = bson.M{"$set": bson.M{"tag": (end + start) / 2}}
			}
		}
		err = c.Update(selector, updata)
		if err != nil {
			log.Println(err)
		}
	}
}

func main() {
	collections := getAllCollections()
	field := "companylogo"
	exist := 0
	for _, coll := range collections {
		resultList, e := GetJobsInfoList(coll, field, exist)
		if e != nil {
			log.Println(e)
		}
		AddTagTask(resultList, coll)
	}

}
