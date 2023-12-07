css = '''
<style>
.chat-message {
    padding: 1rem; 
    border-radius: 0.5rem;
    margin-bottom: 1rem;
    display: flex;
    align-items: flex-start; /* Align to the start for variable content size */
    box-shadow: 0 1px 3px rgba(0,0,0,0.2);
    max-width: 80%;
    min-height: 100px; /* Ensure a minimum height for small messages */
    overflow: hidden; /* Hide overflow */
}
.chat-message.user {
    background-color: #2b313e;
    justify-content: flex-end;
    margin-left: auto;
}
.chat-message.bot {
    background-color: #475063;
    justify-content: flex-start;
    margin-right: auto;
}
.chat-message .avatar {
    flex: 0 0 50px;
}
.chat-message .avatar img {
    width: 50px;
    height: 50px;
    border-radius: 50%;
    object-fit: cover;
}
.chat-message .message {
    flex: 1;
    padding: 0.5rem 1rem;
    color: #fff;
    display: flex;
    flex-direction: column;
    overflow-wrap: break-word; /* New property for word wrapping */
    word-break: break-word; /* Fallback property for word breaking */
}
.chat-message.user .message {
    text-align: left;
}
.chat-message .message ul,
.chat-message .message ol {
    padding-left: 20px; /* Space for bullet points */
    list-style-position: inside; /* Ensure bullets are within the content area */
}

'''

bot_template = '''
<div class="chat-message bot">
    <div class="avatar">
        <img src="https://www.ometrics.com/blog/wp-content/uploads/2018/10/chatbot_thumb.png">
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''

user_template = '''
<div class="chat-message user" style="flex-direction: row-reverse;">
    <div class="avatar">
        <img src="https://i.stack.imgur.com/34AD2.jpg">
    </div>    
    <div class="message">{{MSG}}</div>
</div>
'''