package defs

const (
	MongoUrl         = "127.0.0.1:27017"
	JobsInfoDB       = "jobs_info"
	KeyWordDB        = "notes"
	KeyWordCollction = "keywords"
	// JobsLimitDB = "jobs_limit"
)

// 职位返回体
type ResultList struct {
	JobsInfoList []JobInfo `json:"jobs_info_list"`
	JobsCount    int       `json:"jobs_count"`
}

// 职位列表
type JobInfo struct {
	// _Id          string
	JobName     string `json:"job_name"`
	Salary      string `json:"salary"`
	City        string `json:"city"`
	WorkYear    string `json:"work_year"`
	Education   string `json:"education"`
	CompanyName string `json:"company_name"`
	CompanySize string `json:"company_size"`
	CompanyType string `json:"company_type"`
	CompanyLogo string `json:"company_logo"`
	CompanyUrl  string `json:"company_url"`
	PositionUrl string `json:"position_url"`
}

// type KeyWordList struct {
// 	KeyWords []Keys
// }

type Keys struct {
	KeyWord string `json:"key_word"`
}
