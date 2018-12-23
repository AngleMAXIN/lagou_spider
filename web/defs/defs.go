package defs

// 职位请求体
type JobsRequestBody struct {
	Keyword string `json:"key_word"`
	Salary  string `json:"salary"`
	JobType string `json:"job_type"`
	City    string `json:"city"`
}
