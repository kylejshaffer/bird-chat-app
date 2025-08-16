import { ChatMistralAI } from "@langchain/mistralai";
import { MistralAIEmbeddings } from "@langchain/mistralai";
import { MemoryVectorStore } from "langchain/vectorstores/memory";

import { pull } from "langchain/hub";
import "cheerio";
import { CheerioWebBaseLoader } from "@langchain/community/document_loaders/web/cheerio";
import { Annotation, StateGraph } from "@langchain/langgraph";
import { RecursiveCharacterTextSplitter } from "@langchain/textsplitters";

export function test() {
    const list = ['1', '2', '3'];
    return list;
};