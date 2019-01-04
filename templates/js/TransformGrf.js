    var allpage;
    var requestData;
    var rec;
    var url
    //点击搜索后显示第一页查询结局
    //此时定义全局变量 pagereco(推荐时页码) 和 pageation （筛选时页码） 以及 allpage （总页数）来判断
    var temp = false;
    var pagination = 1; // filter
    var pagereco = 0; //recommendPage

    var salarys = {
        "不限": [],
        "5K": [0, 5],
        "5K-10K": [5, 10],
        "10K-18K": [10, 18],
        "18K-25K": [18, 25],
        "25K以上": [15, 40],

    }

    function selectAjex() {
        // hide old title and jobs info
        Hidititle();
        hidiOldJobsInfo();
        var selectItem = document.getElementsByTagName("select");
        if (selectItem[0].value != "keyword" || selectItem[1].value != "city" ||
            selectItem[2].value != "salary" || selectItem[3].value != "jobtype") {
            
            var jobtype = "fw";
            var salary = salarys[selectItem[2].value];

            if (selectItem[3].value == "不限") {
                jobtype = "";
            }
            requestData = {
                "key_word": selectItem[0].value,
                "city": selectItem[1].value,
                "salary": salary,
                "job_type": jobtype
            };

            temp = true;
            rec[0].style.display = "none";


            for (var i = 1; i < rec.length; i++) {
                rec[i].style.display = "inline";
            }

            pagereco = 1; //进入筛选阶段
        } else {
            alert("请至少选择一项！");
        }

        if (temp) {

            url = "http://127.0.0.1:8080/api-v1/jobs?pn=" + pagereco;
            $.ajax({
                type: 'POST',
                url: url,
                data: JSON.stringify(requestData),
                dataType: 'json',
                success: function(data) {
                    console.log(data);
                    var number = data["jobs_count"];
                    if (number === 0) {
                        alert("没有你查找的数据！");
                        return;
                    }
                    allpage = (number % 9) + 1; //赋值筛选结果总页数

                    var data_list = data["jobs_info_list"];

                    rec[3].innerText = number;

                    for (var i = 0; i < data_list.length; i++) {
                        console.log(data[i]);
                        var html_text = "<li class=\"blank\">" +
                            "<a href=" + data_list[i]["position_url"] + " target=\"view_window\" class=\"jobname\">" + data_list[i]["job_name"] + "</a>" +
                            "<span class=\"pay\">" + data_list[i]["salary"] + "</span>" +
                            "<div>" +
                            "<span class=\"requir\">" + data_list[i]["work_year"] + "/" + data_list[i]["education"] + "</span>" +
                            "</div>" +
                            "<div class=\"company\">" +
                            "<img class=\"img-sty\" href=\"\" src=" + data_list[i]["company_logo"] + " alt=\"company\">" +
                            "<a href=" + data_list[i]["company_url"] + " target=\"view_window\" class=\"companyname\">" + data_list[i]["company_name"] + "</a>" +
                            "<div class=\"companyinfo\">" +
                            "<span href=\"\" style=\"\">" + data_list[i]["company_type"] + "/" + data_list[i]["company_size"] + "/" + data_list[i]["city"] + "</span>" +
                            "</div>" +
                            "</div>" +
                            "</li>";
                        $(".Blank").append(html_text);
                    }
                }
            })
        }

    }

    // hidi jobs info title
    function Hidititle() {
        alert("清空job列表");
        rec = document.getElementsByName("Recommendjob");

        for (var i = 1; i < rec.length; i++) {
            rec[i].style.display = "none";
        }
    }

    //hide jobs info list before reload new jobs list
    function hidiOldJobsInfo() {
        var OldjJobs = document.getElementsByName("blank");
        for (var i = 0; i < OldjJobs.length; i++) {
            OldjJobs[i].style.display = "none";
        }
    }
    // 点击翻页按钮之后显示查询结果
    function checkPage(action) {
        if (action == 'last') {
            if (pagereco == 0) //筛选页数为0即还是显示推荐职业
            {
                if (pagination == 1) //推荐页数是第一页
                {
                    alert("已经是第一页了！");
                } else
                    // 返回上一页数据
                    pagination--;
            } else if (pagereco == 1) //筛选页数是第一页
            {
                alert("已经是第一页了！");
            } else
                // 返回上一页数据
                pagereco--;
        }
        if (action == 'next') {
            if (pagereco == 0) //筛选页数为0即还是显示推荐职业
            {
                if (pagination == 3) //推荐页数是第三页
                {
                    alert("已经是最后一页了！");
                } else
                    // 返回下一页数据
                    pagination++;
            } else if (pagereco == allpage) //筛选页数是最后一页
            {
                alert("已经是最后一页了！");
            } else
                // 返回上一页数据
                pagereco++;
        }
        return true;
    }