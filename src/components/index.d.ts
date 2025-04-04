declare module "components/chat/ChatTile" {
  import { FC } from "react";

  export type ChatMessageType = {
    name: string;
    message: string;
    isSelf: boolean;
    timestamp: number;
  };

  interface ChatTileProps {
    messages: ChatMessageType[];
    accentColor: string;
    onSend?: (message: string) => void;
  }

  const ChatTile: FC<ChatTileProps>;
  export default ChatTile;
}

// Existing declarations for other components
declare module "components/chat/ChatMessage" {
  const ChatMessage: React.FC<any>; // Replace 'any' with the actual props type if known
  export default ChatMessage;
}

declare module "components/chat/ChatMessageInput" {
  const ChatMessageInput: React.FC<any>; // Replace 'any' with the actual props type if known
  export default ChatMessageInput;
}

declare module "components/colorPicker/ColorPicker" {
  const ColorPicker: React.FC<any>; // Replace 'any' with the actual props type if known
  export default ColorPicker;
}

declare module "components/config/AudioInputTile" {
  const AudioInputTile: React.FC<any>; // Replace 'any' with the actual props type if known
  export default AudioInputTile;
}
