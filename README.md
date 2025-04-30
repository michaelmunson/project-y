## Definitions
### Ticket
- A ticket is a request for a task to be completed
- A ticket has a unique id
- A ticket has a status
- A completed ticket has a result

1. LLM with basic completion system (run until stop token)

2. Completion represents tool and arguments
3. Agent calls tool, recieves a ticket id
4. Agent decides either:
  - file a new ticket
  - check status of existing ticket (loop for await)
  - get result of completed ticket
  - return
5. execute either a, b, or c
6. repeat step 4

tools are implemented in FAST API, generates 
