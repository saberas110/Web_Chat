import LeftSide from "../../components/leftSideHome/LeftSide.tsx";
import usePresence from "../../hooks/presence/usePresence.ts";
import useGetUser from "../../hooks/getUser/useGetUser.tsx";


export default function Home(){







const {lodding, user} = useGetUser()
usePresence()

if (!user) {
  return <div>Loading user...</div>;
}

    return(
        <>
                <LeftSide />

        </>
    )
}