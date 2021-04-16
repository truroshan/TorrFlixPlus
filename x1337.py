import requests
from bs4 import BeautifulSoup

def search(keyword,quality):
	URL = 'https://1337x.to/sort-search/{}/seeders/desc/1/'.format(keyword)
	response = requests.get(URL,headers = {'User-Agent':'mi @roshan'})
	if response.status_code != 200:
		print("requests error")
		exit()
	soup = BeautifulSoup(response.text,'lxml')
	movies = soup.find("tbody")

	moviesData = list()

	i = 1
	try:
		for movie in movies.findAll('tr'):
			post = movie.findAll('td')

			movieDetails = dict()

			movieDetails['name'] = post[0].findAll('a')[1].string
			movieDetails['url'] = post[0].findAll('a')[1]['href']
			movieDetails['seeder'] = int(post[1].string)
			movieDetails['leecher'] = int(post[2].string)
			movieDetails['date'] = post[3].string
			movieDetails['uploader'] = post[5].string
			movieDetails['size'] = converSize(post[4].text) #str(post[4].text).split('B')[0] + 'B'
			movieDetails['size_in'] = 'MB'

			if i == 3:
				break
			if quality in movieDetails['name']:
				url = movieDetails['url']
				postHtml = requests.get('https://1337x.to'+url).text
				movieDetails['magnet'] = getMagnet(postHtml)
				movieDetails['files'] = getFiles(postHtml)
				moviesData.append(movieDetails)
				i += 1
		
	except:
		print("Movie not available sed")
		exit()
	return moviesData

def converSize(size):
	if 'MB' in size:
		if ',' in size:
			return int(size.split(',')[0] + size.split(',')[1].split('.')[0] )
		return int(size.split('.')[0])
	if 'GB' in size:
		return int(size.split('.')[0]) * 1000 + int(size.split('.')[1].split()[0]) * 100

def getMagnet(postHtml):
	soup = BeautifulSoup(postHtml,'lxml')
	magnet = soup.find(class_ = 'col-9 page-content').find('a')['href']
	return magnet

def getFiles(postHtml):
    soup =BeautifulSoup(postHtml,'lxml')
    files = soup.find('div',class_ = 'tab-pane file-content').findAll('li')

    decideMovieShow = 0
    fileList = dict()
    fileList['file'] = list()
    for index,file in enumerate(files):
        if 'mkv' in file.text or 'mp4' in file.text and 'sample' not in file.text:
            decideMovieShow += 1   		
        fileList['file'].append({index+1:file.text})
    
    if decideMovieShow <= 2:
        fileList['type'] = 'movie'
    else:
        fileList['type'] = 'show'

    return fileList
def main():
	print(search('limitless hindi',quality='720'))
	

if __name__ == '__main__':
	main()