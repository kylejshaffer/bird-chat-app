import { Flex, Text } from '@chakra-ui/react';

function Message(props) {
    return (
      <Flex
        p={4}
        bg={props.actor === 'user' ? 'blue.500' : 'gray.100'}
        color={props.actor === 'user' ? 'white' : 'gray.600'}
        borderRadius="lg"
        w="fit-content"
        alignSelf={props.actor === 'user' ? 'flex-end' : 'flex-start'}
      >
        <Text>{props.text}</Text>
      </Flex>
    );
  };

export default Message;