import openai from './config/open-ai.js'
import readlineSync from 'readline-sync'
import colors from 'colors'

import fs from 'fs'

/*
  * This script leverages the openai api to create a chatbot
  * this script records teh converstaion history during the session 
  * then the conversation history is saved to disk after each interaction 
  * leveraging the 'fs' module in a file labled conversation.log
  * if the file does not exist it will be created automatically
  */ 

// Function to interact with the chatbot
const chat = async () => {

  const greetingMessage = 'ChatBot: Hello, how can I help you today?'

  console.log(colors.bold.green(greetingMessage))

  const conversationHistory = [] // Store conversation history



  
  while (true) {
    // get user input 
    const userInput = readlineSync.question(colors.yellow('User: '))


    try {

      // Construct messages by iterating over the history
      const messages = conversationHistory.map(([role, content]) => ({
        role,
        content,
      }))


      // Add latest user input
      messages.push({ role: 'user', content: userInput })


      // Call the API with user input & history
      const completion = await openai.createChatCompletion({
        model: 'gpt-3.5-turbo',
        messages: messages,
      })

      
      // Get completion text/content
      const completionText = completion.data.choices[0].message.content


      if (userInput.toLowerCase() === 'exit') {
        console.log(colors.green('Bot: ') + completionText)
        return
      }


      console.log(colors.green('Bot: ') + completionText)
      

      // Add user input to the conversation history
      conversationHistory.push(['user', userInput])

      //add Chatbot reply to the conversation history
      conversationHistory.push(['assistant', completionText])

      // Log conversationHistory to a file
      fs.appendFileSync("conversationHistory.log", conversationHistory.join("\n") + "\n")

    } catch (err) {
      console.error(colors.red('Error: ' + err.mesage()))
      return
      // console.error(colors.red(error))
    }
  }
}

chat()
