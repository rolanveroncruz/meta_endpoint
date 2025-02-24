__Feb 24, 2025__
A few days ago, I got google's gemini flash-2.0 to do ocr on a sample eTap receipt. It successfully
extracted key information. Today, i tried using llama3.2-vision. Unfortunately, I still need to 
parse its output, which is looks like it would be difficult to do.
And since the purpose of this exercise is to to serve FB messenger chats, it's down to running ollama
in the cloud vs. just using Google Gemini's API. The latter at this time is good enough.
Will work on digital signing first.



__Feb 20, 2025__
We can now receive text messages. But we should review the payload specs to make
sure of things. But maybe more importantly (for now), we should learn how to:
1. get the identity of the message sender from the sender id.
2. learn to reply.


__Feb 18,2025__

I've finally started implementing this fb_messenger endpoint. The thing is i foresee
some difficulties in testing it: I'll either have to learn __cloudflare tunnels__ or deploy 
this already to an aws ec2 instance. The payoff is just too long or expensive (deploying to AWS
also requires getting the domain name and ssl cert running.). Maybe i can 
first take a look at the fb messenger quick start to see how 
to get something running quickly?

