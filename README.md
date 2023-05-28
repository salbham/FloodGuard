# FloodGuard
<p>Bangalore, also known as the Silicon Valley of India, is one of the fastest-growing cities in the country. While the city has witnessed rapid urbanization, it remains plagued with inadequate infrastructure and a poor drainage system which has contributed to frequent occurrences of waterlogging during the monsoon season. Waterlogging causes a huge inconvenience to residents, disrupting transportation and also posing health hazards in the form of accidents to residents who have to travel through such waterlogged areas.</p>
<p>We propose to help folks tackle this problem by collecting real-time data on waterlogging incidents as they occur and make them available and visible in an easy manner. And this is where crowdsourcing comes in the form of Twitter! Twitter provides a platform where users frequently share information and updates in real-time. So we decided to aggregate and analyze tweets that spoke about waterlogging, used OpenAI to determine if the tweet reported waterlogging in a certain area and plotted this data onto a map that can be referred to by residents while they planned their commute during heavy rains, thus minimizing the adverse effects of waterlogging.
</p>
![alt text](https://github.com/salbham/FloodGuard/blob/main/MapFinalImage.png)<br><br>
<p><b>Tech Stack Used</b><br>
* Used snscape which is a python library to scrape the twitter data
* Got the relevant tweets based on location and flooding or water logging information
* Used OPENAI to do NLP and sentiment analysis on the tweet content body and thus classified it as water logged or not basis the location 
</p>



