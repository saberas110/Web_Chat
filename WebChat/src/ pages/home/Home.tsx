import LeftSide from "../../components/leftSideHome/LeftSide.tsx";
import usePresence from "../../hooks/presence/usePresence.ts";


export default function Home(){

usePresence()



    return(
        <>
            <LeftSide />
        </>
    )
}