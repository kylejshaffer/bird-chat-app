import React, { useRef, useState } from "react";
import { Button, ChakraProvider, Heading,
         Input, HStack, VStack, Stack, Text } from "@chakra-ui/react";
import { Menu, MenuButton, MenuList, MenuItem, Link } from "@chakra-ui/react";
import ChatPane from "./components/ChatPane";

function App() {
  const urlMap = [
    "https://ornithology.com/the-snakebird/",
    'https://ornithology.com/the-secretarybird/',
    'https://ornithology.com/12003-2/',
  ];

  const [urlState, setUrl] = useState(urlMap[0]);
  const [messageList, setMessageList] = useState([]);

  const iFrameRef = useRef(null);
  const userInputRef = useRef(null);

  const handleMenuClick = (e) => {
    console.log("Raw event input:");
    console.log(e);
    console.log("URL state value:");
    setUrl(e.target.value);
    console.log(urlState);

    fetch("https://bird-chat-app.vercel.app/site_change", {
      method: "POST",
      headers: {
        'Content-Type' : 'application/json'
      },
      body: JSON.stringify({"url": e.target.value}),
    }).then(res => res.json())
    .then(jsonResp => console.log(jsonResp));
  };

  async function handleSubmit(e) {
    e.preventDefault();
    const iFrameElement = iFrameRef.current;
    console.log("IFRAME:", iFrameElement.src);
    console.log(userInputRef.current.value);

    const userChat = userInputRef.current.value;
    if (!userChat) return;
    console.log("from handleSubmit:");
    const ragData = {
      'url': iFrameElement.src,
      'question': userChat,
    };
    console.log(ragData);

    setMessageList((prevList) => [...prevList, {agent: "user", text: "👤  " + userChat}]);
    userInputRef.current.value = "";

    fetch("https://bird-chat-app.vercel.app/query", {
      method: "POST",
      headers: {
        'Content-Type' : 'application/json'
      },
      body: JSON.stringify(ragData),
    }).then(resp => resp.json())
    .then(
      botResponse => setMessageList((prevList) =>  [...prevList, {agent: "bot", text: "🤖  " + botResponse.answer}])
    );
  };

  return (
    <ChakraProvider>
      <VStack
        h="100%"
        mt="2%"
        py={0}
        justify="center"
        align="center"
      >
        <Heading>Bird Chat 🦜</Heading>
        <Text w="95vh">
          This app allows you to browse blog posts about several bird species on the right-hand pane,
          and enter questions to an AI agent in the left chat pane. Specifically, this app uses a 
          Retrieve-and-Generate <b>(RAG)</b> LLM model to ground chat model responses in the content of the
          site at the right. You can read more about the technical details <Link color="blue.400" href="https://github.com/kylejshaffer/bird-chat-app/blob/main/README.md" isExternal>here</Link>.
        </Text>
        <HStack
         mt="1%"
         align="center"
         justify="center">
          <VStack>
            <ChatPane messageList={messageList} />
            <HStack w={"100%"}>
              <Input
                bg="white"
                placeholder="Start typing to begin..."
                ref={userInputRef}
              />
              <Button onClick={handleSubmit} bg={"blue.400"} textColor="white" type="submit">
                Submit
              </Button>
            </HStack>
          </VStack>

          <VStack w="100vh" h="80vh">
            <Stack borderWidth="3px" w="70vh" h="70vh">
              <iframe src={urlState}
                id="querySite"
                ref={iFrameRef}
                width="100%"
                height="650px"
                title="Embedded website">
              </iframe>
            </Stack>
            <VStack>
              <Heading as='h3' size='sm'>Select a bird to learn about</Heading>
              <Menu>
                <MenuButton mb={10} bgColor="blue.400" textColor="white" as={Button}>
                    Select A Bird
                </MenuButton>
                <MenuList onClick={handleMenuClick}>
                    <MenuItem value={urlMap[0]}>Snakebird</MenuItem>
                    <MenuItem value={urlMap[1]}>Secretary Bird</MenuItem>
                    <MenuItem value={urlMap[2]}>Swans</MenuItem>
                </MenuList>
              </Menu>

            </VStack>
          </VStack>
        </HStack>
      </VStack>
    </ChakraProvider>
  );
};

export default App;
