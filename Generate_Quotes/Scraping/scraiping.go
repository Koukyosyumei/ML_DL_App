package main

import _ "fmt"

import (
	"database/sql"
	"fmt"

	"github.com/PuerkitoBio/goquery"
	_ "github.com/mattn/go-sqlite3"
)

func scrape_onepage(target_url string, base_url string, db *sql.DB) (result string) {
	/* Summary line
		名言とその著者名をスクレイピングする

		Args
				target_url (string) : 最初に接続するためのurl
				base_url   (string) : スクレイピングするサイトのurl
				db                  : 保存用のデータベース

		Returns
				next_url            : 次のページのurl


	*/

	urls := []string{}
	var next_url string
	// get document
	doc, err := goquery.NewDocument(target_url)
	if err != nil {
		fmt.Println(err.Error())
	}

	// search
	doc.Find(".quote").Each(func(i int, s *goquery.Selection) {

		//fmt.Printf("Title: %s %s\n", s.Find(".caption").Text(), s.Find(".by").Text())
		//fmt.Printf(s.Find(".author").Text())
		url, _ := s.Find("a").Attr("href")
		url = base_url + url
		urls = append(urls, url)
		//fmt.Printf("%s\n\n", strings.Replace(s.Find(".text").Text(), "\n", "", -1))

		_, err := db.Exec(
			`INSERT INTO QUOTES (QUOTE, AUTHOR) VALUES (?, ?)`,
			s.Find(".text").Text(),
			s.Find(".author").Text(),
		)
		if err != nil {
			fmt.Print(2)
			panic(err)
		}

	})

	doc.Find(".next").Each(func(i int, s *goquery.Selection) {
		next_url, _ = s.Find("a").Attr("href")
	})

	for i := range urls {
		doc_aut, err := goquery.NewDocument(urls[i])
		if err != nil {
			fmt.Print("\n", "child url scarapping failed", "\n")
		}
		doc_aut.Find(".author-details").Each(func(i int, s *goquery.Selection) {

			//fmt.Printf("Title: %s %s\n", s.Find(".caption").Text(), s.Find(".by").Text())
			//fmt.Printf(s.Find(".author-born-date").Text())
			//fmt.Printf(s.Find(".author-born-location").Text())
			//fmt.Printf("%s\n\n", strings.Replace(s.Find(".author-description").Text(), "\n", "", -1))

			_, err := db.Exec(
				`INSERT INTO AUTHORS (AUTHOR_BORN_DATE, AUTHOR_BORN_LOCATION, DETAIL) VALUES (?, ?, ?)`,
				s.Find(".author-born-date").Text(),
				s.Find(".author-born-location").Text(),
				s.Find(".author-description").Text(),
			)
			if err != nil {
				fmt.Printf("3")
				panic(err)
			}

		})
	}
	next_url = base_url + next_url
	return next_url
}

func main() {
	db, err := sql.Open("sqlite3", "./test.db")
	if err != nil {
		fmt.Printf("0")
		panic(err)
	}

	// テーブル作成
	_, err = db.Exec(
		`CREATE TABLE IF NOT EXISTS "QUOTES" ("QUOTE" VARCHAR(255),
    "AUTHOR" VARCHAR(255))`,
	)

	if err != nil {
		fmt.Printf("1")
		panic(err)
	}

	_, err = db.Exec(
		`CREATE TABLE IF NOT EXISTS "AUTHORS" (
    "AUTHOR_BORN_DATE" VARCHAR(255), "AUTHOR_BORN_LOCATION" VARCHAR(255), "DETAIL" VARCHAR(255))`,
	)

	if err != nil {
		fmt.Printf("1")
		panic(err)
	}

	base_url := "http://quotes.toscrape.com"
	next_url := "http://quotes.toscrape.com"

	x := 100

	for x > 0 {
		next_url = scrape_onepage(next_url, base_url, db)
	}
}
