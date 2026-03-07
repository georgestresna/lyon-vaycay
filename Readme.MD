# 🚄 LyonVaycay (Work In Progress 🚧)

**Quick heads up:** This app is currently under construction and not entirely complete yet!

### What is this?

I am building a smart weekend-trip finder. Instead of just blindly searching for the "cheapest" bus ticket, this app scrapes Flixbus data across multiple cities for the next 4 weeks to find the absolute best "Worth It" trips from Lyon.

It works by building a massive 3D matrix of ticket prices and travel times, and then runs them through a custom scoring algorithm.

The algorithm judges trips based on two things:

1. **Price:** How cheap is the ticket compared to this city's usual 4-week baseline?
2. **Time:** How much actual vacation time do you get at the destination before you have to come back?

It then spits out the top-scored trips and displays them on a clean web dashboard.

### The Tech Stack

* **Backend & Scraping:** Python (Selenium)
* **Data Structure:** Flat JSON / MongoDB (to store the 3D Matrix data)
* **Web Server:** FastAPI & Uvicorn
* **Frontend:** to be continues

---
*Note: Still tweaking the web server and dynamic HTML rendering. More updates coming soon!*
