<!-- PROJECT LOGO -->
<div align="center">
  <a>
    <img src="https://github.com/user-attachments/assets/5b50da49-55db-4239-934d-fcd9ece751f1" alt="Logo" height="300">
  </a>
  <h1>GrabBuddy</h1>
  <p>Economic empowerment through AI</p>
</div>

<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#about-the-project">About The Project</a></li>
    <li><a href="#data-utilization">Data Utilization</a></li>
    <li><a href="#personalization-strategies">Personalization Strategies</a></li>
    <li><a href="#ui-figma-design">UI Figma Design</a></li>
    <li><a href="#solution-architecture">Solution Architecture</a></li>
    <li><a href="#installation">Installation</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
    <li><a href="#fun-fact">Fun Fact</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->

## About The Project
<div align="center">
  <img src="https://github.com/user-attachments/assets/ff428c8d-18be-4348-86fe-a78239a86a57" alt="Slides Preview" height="300">
</div>

<div align="center">
  <a href='https://1drv.ms/p/c/93d0dcb6fb3b029b/EYAch3l00mlMqpaQRrBdCBkBZqK9pAzKfdJC0AbdqUOv9A'> CLICK ME FOR THE SLIDES </a> 
</div>

<div align="center">
  <a href='https://imailsunwayedu-my.sharepoint.com/:v:/g/personal/22112478_imail_sunway_edu_my/EU65ovys9_9PnwO6WoOHix0Bghf81vrE-M3-jxoCASHrbQ?nav=eyJyZWZlcnJhbEluZm8iOnsicmVmZXJyYWxBcHAiOiJPbmVEcml2ZUZvckJ1c2luZXNzIiwicmVmZXJyYWxBcHBQbGF0Zm9ybSI6IldlYiIsInJlZmVycmFsTW9kZSI6InZpZXciLCJyZWZlcnJhbFZpZXciOiJNeUZpbGVzTGlua0NvcHkifX0&e=rQdBZE'> CLICK ME FOR THE DEMO VIDEO </a> 
</div>
  
**GrabBuddy** is a solution project for UMHackathon 2025 by Team 418, it is a platform to further empower entrepreneurs working with grab by leveraging Generative AI to create smart, intuitive chat-based assistants. These AI-driven interfaces allow for actionable insights and proactive guidance directly to merchants, enabling better business decisions and streamlined operations.


### Problem Statement

The goal is to develop an intelligent, chat-based AI assistant that proactively provides merchant-partners with **valuable insights**, **personalized guidance**, and **operational alerts**.

## Data Utilization

The data used in this project can be found [here](https://drive.google.com/drive/folders/1q8wpploa41fXcw823SSEkb6xfyDQcsVd?usp=drive_link).

Some of the data were provided by the hosts of UMHackathon, while some were generated using AI.

## Personalization Strategies
1. **Customer Feedback Personalization** <br/>

   Strategy: Analyze recurring themes in reviews to segment customers by satisfaction level, preferences, and complaints.

   Action: Automatically customize promotions or responses (e.g., vouchers for those who complain about packaging or delays).

   Outcome: Builds customer trust and shows responsiveness to feedback.

3. **Dynamic Offer Personalization** <br/>
  
   Strategy: Identify best-selling and underperforming items by customer segment and time of day/week.

   Action: Personalize homepage layouts, upsell combos, or push notifications based on trending products for each user.

   Outcome: Boosts sales through timely, relevant product placements.

4. **Smart Bundle Customization** <br/>

   Strategy: Use product list insights to tailor bundle deals based on frequently purchased items.

   Action: Offer auto-generated bundles (e.g., “Your usual lunchtime combo”) or recommend missing items in a customer's cart.

   Outcome: Increases basket size and inventory turnover.

6. **Purchase History Personalization** <br/>

   Strategy: Convert past receipts into customer profiles (e.g., frequency, spend level, product categories).

   Action: Enable merchants to offer loyalty perks (e.g., “5th order discount”) or tailored re-order suggestions.

   Outcome: Encourages repeat orders and builds long-term loyalty.

8. **Multilingual Support** <br/>

   Strategy: Automatically localize communication (promotions, review replies, chat support) to the customer’s preferred language.

   Outcome: Improves accessibility and engagement for diverse customer bases.

## UI Figma Design
<a>
  <img src="https://github.com/user-attachments/assets/b9b1229d-7356-4844-96be-22c9ea965ba3" alt="Overview" height="300">
</a>
<a>
  <img src="https://github.com/user-attachments/assets/070123df-ae41-4716-83de-25cdd5d7aed2" alt="Chat" height="300">
</a> <br/>
<a href='https://www.figma.com/proto/1NRKS2Fl2SR0sYbWPWOrhZ/UM-Hackathon?page-id=0%3A1&node-id=2506-4757&p=f&viewport=-341%2C-
  261%2C0.2&t=FepnjYQum9eWRZhD-1&scaling=scale-down&content-scaling=fixed&starting-point-node-id=2506%3A4757'> CLICK ME FOR THE FIGMA PROTOTYPE</a> 


## Solution Architecture

<div align="center">
  <a>
    <img src="https://github.com/user-attachments/assets/2de685bd-d8a1-44bf-b7e7-d2fd89709dda" alt="Solution Architecture Diagram" height="300">
  </a>
</div>

**Client**
- [SvelteKit](https://kit.svelte.dev/)
- [ApexCharts](https://apexcharts.com/)
- [Tailwind](https://tailwindcss.com/)
- [TypeScript](https://www.typescriptlang.org/)

**Server**
- [FastAPI](https://fastapi.tiangolo.com/)
- [Pydantic](https://docs.pydantic.dev/latest/)
- [Pydantic AI](https://ai.pydantic.dev/)
- [OpenCV](https://opencv.org/)
- [Ollama](https://ollama.com/)

**Database**
- [PostgreSQL](https://www.postgresql.org/)
- [Docker](https://www.docker.com/)
  
## Installation

This repository includes both the codebase for the frontend and the backend, follow the steps mentioned below to run the code:
### Client
<a href='https://github.com/Spimy/UMHackathon/blob/Readme/client/README.md'> CLICK HERE FOR THE SETUP STEPS FOR FRONTEND </a>
### Server
<a href='https://github.com/Spimy/UMHackathon/blob/Readme/server/README.md'> CLICK HERE FOR THE SETUP STEPS FOR BACKEND </a>

Team 418 members:

- [Justin Yong Wenn Weii](https://github.com/Justin-yww) - Product Manager
- [William Law Hong Waye (Spimy)](https://github.com/Spimy) - Tech Lead
- [Alex Chee Kai Hong](https://github.com/datgai) - AI Engineer
- [Joshua Edwin Rene Bonham](https://github.com/JBBru-helloworld) - UI Designer

Teamwork makes the dream work

## Fun Fact

The name **418** refers to this [easter egg](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/418).
