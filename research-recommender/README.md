*********************************************************************
Phase 1 – Core Search & Display (Completed / mostly done)
*********************************************************************
> Web app with a search bar for papers.
> Fetch papers from APIs like arXiv.
> Display title, authors, abstract, published date, and source.
> Display in responsive cards.
> Dark/Light mode toggle with filters synced.
> Filters: Source and Year.
> Fully responsive and adjusts to window size.


*********************************************************************
Phase 2 – API & Backend Improvements
*********************************************************************
Enhance backend API (fetch_api.py / Flask) to:
- Support multiple sources: arXiv, IEEE Xplore, Semantic Scholar.
- Include published/submitted date in a uniform format.
- Return source reliably.
- Support pagination for large result sets.
- Optional: caching to reduce repeated API calls.
Add error handling for:
- Network issues
- Empty results
- API rate limits


*********************************************************************
Phase 3 – Advanced Features / Enhancements
*********************************************************************
- Full-text search and keyword highlighting in abstracts.
- Sorting options: newest first, oldest first, author name.
- Additional filters:
Author name
Topic / keywords
Journal / conference
User accounts (optional):
Save favorite papers
Track search history

Improved UI/UX:
- Hover effects on cards
- Collapsible abstracts
- Smooth transitions for light/dark mode
Performance:
- Infinite scroll or “Load more” button
- Optimize API requests for large queries


*********************************************************************
Phase 4 – Optional Machine Learning / Recommendation
*********************************************************************
- Use NLP embeddings to suggest related papers based on:
User search history
Papers the user clicks on

- Implement cosine similarity or pre-trained embeddings from:
sentence-transformers
OpenAI embeddings API

- Show “You may also like” suggestions below each paper.


*********************************************************************
Phase 5 – Deployment / Community Use
*********************************************************************
- Deploy frontend + backend using:
Vercel or Netlify for React
Heroku / Render / Railway for Flask backend

- Optional: add Docker for easy deployment.
Share with students/researchers for testing.