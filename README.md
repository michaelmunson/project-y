1. LLM with basic completion system (run until stop token)
2. Completion represents tool and arguments
3. Agent calls tool, recieves a ticket id
4. Agent decides either:
  a. await ticket completion
  b. file a new ticket
  c. check status of existing ticket
  d. return
5. execute either a, b, or c
6. repeat step 4

tools are implemented in FAST API, generates 
