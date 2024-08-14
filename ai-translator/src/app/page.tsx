import AiChat from "@/components/AiChat";
import Header from "@/components/Header";

const styles = {
  flex_container: "flex h-full w-full flex-col items-center gap-6 bg-default-background pt-12 pr-6 pl-6",
  chat_container: "flex w-full max-w-[576px] grow shrink-0 basis-0 flex-col items-start relative",
};

export default function Home() {

  return (
    <div className={styles.flex_container}>
      <Header />
      <div className={styles.chat_container}>
        <AiChat />
      </div>
    </div>
  );
}
