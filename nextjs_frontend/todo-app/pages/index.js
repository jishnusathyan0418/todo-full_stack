import Head from "next/head"
import Layout from '../components/layout';
import ToDoList from '../components/todo-list';

export default function Home() {
  return (
    <div>
      <Head>
        <title>Full Stack ToDO</title>
        <meta name="description" content="full stack todo" />
        <link rel="icon" href="/favicon.ico"/>
      </Head>
      <Layout>
        <ToDoList />
      </Layout>
    </div>
  )
}