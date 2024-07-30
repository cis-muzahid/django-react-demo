import axios from 'axios'


const API_URL = process.env.REACT_APP_API_URL

export const DUMMY_DATA_URL = `${API_URL}/dummy-data/`

export async function getData(token: string): Promise<any> {
  try {
    const response = await axios.get(DUMMY_DATA_URL, {
      headers: {
        Authorization: `Bearer ${token}`,  
      },
    });

    return response.data;
  } catch (error) {
    console.log(error)
  }
}