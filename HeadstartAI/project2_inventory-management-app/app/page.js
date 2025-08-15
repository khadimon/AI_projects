'use client'

import { useState, useEffect } from 'react'
import { Box, Stack, Typography, Button, Modal, TextField, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, ThemeProvider, createTheme, InputAdornment } from '@mui/material'
import { Search as SearchIcon, Add as AddIcon, Delete as DeleteIcon } from '@mui/icons-material'
import { firestore } from '../firebase'
import {
  collection,
  doc,
  getDocs,
  query,
  setDoc,
  deleteDoc,
  getDoc,
  serverTimestamp,
  writeBatch,
} from 'firebase/firestore'

const theme = createTheme({
  palette: {
    primary: {
      main: '#2e7d32', // dark green
    },
    secondary: {
      main: '#4caf50', // light green
    },
    background: {
      default: '#e8f5e9', // very light green
    },
  },
  typography: {
    fontFamily: "'Roboto Mono', 'Courier New', monospace",
    h3: {
      fontWeight: 700,
    },
    h4: {
      fontWeight: 700,
    },
    body1: {
      fontWeight: 500,
    },
    button: {
      fontWeight: 700,
    },
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          textTransform: 'none',
        },
      },
    },
  },
});

const style = {
  position: 'absolute',
  top: '50%',
  left: '50%',
  transform: 'translate(-50%, -50%)',
  width: 400,
  bgcolor: '#e8f5e9',
  border: '2px solid #2e7d32',
  boxShadow: 24,
  p: 4,
  display: 'flex',
  flexDirection: 'column',
  gap: 3,
}

export default function Home() {
    const [inventory, setInventory] = useState([])
    const [filteredInventory, setFilteredInventory] = useState([])
    const [open, setOpen] = useState(false)
    const [itemName, setItemName] = useState('')
    const [error, setError] = useState(null)
    const [searchTerm, setSearchTerm] = useState('')

    const updateInventory = async () => {
        try {
            const inventoryRef = collection(firestore, 'inventory')
            const snapshot = await getDocs(query(inventoryRef))
            const inventoryList = snapshot.docs.map(doc => {
                const data = doc.data()
                return { 
                    name: doc.id, 
                    quantity: data.quantity, 
                    price: parseFloat(data.price),
                    totalPrice: (data.quantity * data.price).toFixed(2),
                    lastUpdated: data.lastUpdated ? data.lastUpdated.toDate() : new Date()
                }
            }).sort((a, b) => a.name.localeCompare(b.name))
            setInventory(inventoryList)
            console.log("Fetched inventory:", inventoryList)
        } catch (error) {
            console.error("Error updating inventory:", error)
            setError("Failed to fetch inventory. Please try again.")
        }
    }
      
    useEffect(() => {
        updateInventory()
    }, [])

    useEffect(() => {
        const filtered = inventory.filter(item => 
            item.name.toLowerCase().includes(searchTerm.toLowerCase())
        )
        setFilteredInventory(filtered)
    }, [searchTerm, inventory])

    const addItem = async (item) => {
        if (!item || typeof item !== 'string' || item.trim() === '') {
            console.error("Invalid item name")
            setError("Invalid item name")
            return
        }
        try {
            const docRef = doc(firestore, 'inventory', item)
            const docSnap = await getDoc(docRef)
            if (docSnap.exists()){
                const {quantity, price} = docSnap.data()
                await setDoc(docRef, {
                    quantity: quantity + 1, 
                    price, 
                    lastUpdated: serverTimestamp()
                }, { merge: true })
            }
            else {
                const price = (Math.random() * 4 + 1).toFixed(2) // Generate random price between $1 and $5
                await setDoc(docRef, {
                    quantity: 1, 
                    price: parseFloat(price), 
                    lastUpdated: serverTimestamp()
                })
            }
            await updateInventory()
        } catch (error) {
            console.error("Error adding item:", error)
            setError("Failed to add item. Please try again.")
        }
    }

    const removeItem = async (item) => {
        if (!item || typeof item !== 'string' || item.trim() === '') {
            console.error("Invalid item name")
            setError("Invalid item name")
            return
        }
        try {
            const docRef = doc(firestore, 'inventory', item)
            const docSnap = await getDoc(docRef)
            if (docSnap.exists()) {
                const {quantity} = docSnap.data()
                if (quantity <= 1) {
                    await deleteDoc(docRef)
                }
                else {
                    await setDoc(docRef, {
                        quantity: quantity - 1, 
                        lastUpdated: serverTimestamp()
                    }, { merge: true })
                }
            }
            await updateInventory()
        } catch (error) {
            console.error("Error removing item:", error)
            setError("Failed to remove item. Please try again.")
        }
    }

    const removeAllItems = async () => {
        try {
            const batch = writeBatch(firestore)
            const inventoryRef = collection(firestore, 'inventory')
            const snapshot = await getDocs(query(inventoryRef))
            
            snapshot.docs.forEach((doc) => {
                batch.delete(doc.ref)
            })

            await batch.commit()
            await updateInventory()
            console.log("All items removed successfully")
        } catch (error) {
            console.error("Error removing all items:", error)
            setError("Failed to remove all items. Please try again.")
        }
    }

    const handleOpen = () => setOpen(true)
    const handleClose = () => setOpen(false)

    const handleAddItem = () => {
        addItem(itemName)
        setItemName('')
        handleClose()
    }

    const handleKeyPress = (event) => {
        if (event.key === 'Enter') {
            event.preventDefault() // Prevent default Enter key behavior
            handleAddItem()
        }
    }

    return (
        <ThemeProvider theme={theme}>
            <Box
              width="100vw"
              minHeight="100vh"
              display={'flex'}
              flexDirection={'column'}
              alignItems={'center'}
              gap={2}
              py={4}
              bgcolor="background.default"
            >
                <Box
                  border="2px solid #2e7d32"
                  borderRadius="8px"
                  p={3}
                  mb={2}
                  width="80%"
                  maxWidth={800}
                  bgcolor="white"
                >
                    <Typography color="primary" variant="h3" component="h1" align="center" gutterBottom>
                        🍏 Grocery Store 🍏
                    </Typography>
                    <Typography color="primary" variant="h3" component="h1" align="center">
                        inventory_list
                    </Typography>
                </Box>
                <Stack direction="row" spacing={2} width="80%" maxWidth={1200} justifyContent="space-between">
                    <Stack direction="row" spacing={2}>
                        <Button 
                            variant="contained" 
                            color="primary" 
                            onClick={handleOpen}
                            startIcon={<AddIcon />}
                        >
                            New Item
                        </Button>
                        <Button 
                            variant="contained" 
                            color="error" 
                            onClick={removeAllItems}
                            startIcon={<DeleteIcon />}
                        >
                            Remove All
                        </Button>
                    </Stack>
                    <TextField
                        variant="outlined"
                        placeholder="Search inventory..."
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                        InputProps={{
                            startAdornment: (
                                <InputAdornment position="start">
                                    <SearchIcon color="primary" />
                                </InputAdornment>
                            ),
                        }}
                        sx={{ flexGrow: 1, maxWidth: 300 }}
                    />
                </Stack>

                <TableContainer component={Paper} sx={{ width: '80%', maxWidth: 1200, flexGrow: 1, mb: 2, bgcolor: 'white' }}>
                    <Table stickyHeader aria-label="inventory table">
                        <TableHead>
                            <TableRow>
                                <TableCell sx={{ bgcolor: '#4caf50', color: 'white' }}>Item</TableCell>
                                <TableCell align="right" sx={{ bgcolor: '#4caf50', color: 'white' }}>Quantity (lbs)</TableCell>
                                <TableCell align="right" sx={{ bgcolor: '#4caf50', color: 'white' }}>Total Price</TableCell>
                                <TableCell align="right" sx={{ bgcolor: '#4caf50', color: 'white' }}>Last Updated</TableCell>
                                <TableCell align="right" sx={{ bgcolor: '#4caf50', color: 'white' }}>Actions</TableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {filteredInventory.map((item) => (
                                <TableRow key={item.name} sx={{ '&:nth-of-type(odd)': { bgcolor: '#e8f5e9' } }}>
                                    <TableCell component="th" scope="row">
                                        {item.name.charAt(0).toUpperCase() + item.name.slice(1)}
                                    </TableCell>
                                    <TableCell align="right">{item.quantity}</TableCell>
                                    <TableCell align="right">${item.totalPrice}</TableCell>
                                    <TableCell align="right">{item.lastUpdated.toLocaleString()}</TableCell>
                                    <TableCell align="right">
                                        <Button variant="contained" color="secondary" onClick={() => addItem(item.name)} sx={{ mr: 1 }}>
                                            Add
                                        </Button>
                                        <Button variant="contained" color="primary" onClick={() => removeItem(item.name)}>
                                            Remove
                                        </Button>
                                    </TableCell>
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                </TableContainer>
                {error && <Typography color="error">{error}</Typography>}
                <Modal
                    open={open}
                    onClose={handleClose}
                    aria-labelledby="modal-modal-title"
                    aria-describedby="modal-modal-description"
                >
                    <Box sx={style}>
                        <Typography id="modal-modal-title" variant="h6" component="h2" color="primary">
                            Add Item
                        </Typography>
                        <Stack width="100%" direction={'row'} spacing={2}>
                            <TextField
                                id="outlined-basic"
                                label="Item"
                                variant="outlined"
                                fullWidth
                                value={itemName}
                                onChange={(e) => setItemName(e.target.value)}
                                onKeyPress={handleKeyPress}
                            />
                            <Button
                                variant="contained"
                                color="primary"
                                onClick={handleAddItem}
                            >
                                Add
                            </Button>
                        </Stack>
                    </Box>
                </Modal>
            </Box>
        </ThemeProvider>
    )  
}