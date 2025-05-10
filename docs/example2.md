# Query
Give me an update on the status of my current projects


# Classic Agent
1. give me a list of all of the different I have
  --> /email-feeds/all
  ----------------
  newsletters
  slack updates
  github updates
2. --> /email-feeds/github-updates?range=today
  ----------------
  feed-item[]
3. --> Promise.all(feed-item.map(s3.get(item)))
  ----------------
  feed-item-content[]
4. --> /llm "Here is the content of the feed items: {feed-item-content[]}, generate a summary of the updates. What is everyone working on?"
  ----------------
  summary
5. return summary

# Recursive Agent
1. give me a list of the relevant feed items that would relate to "current projects"
  ----------------
  feed-item-content[]
2. --> /llm "Here is the content of the feed items: {feed-item-content[]}, generate a list of the current projects. What is everyone working on?"
  ----------------
  summary
3. return summary