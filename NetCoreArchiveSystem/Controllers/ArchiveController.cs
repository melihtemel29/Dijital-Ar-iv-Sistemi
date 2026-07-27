using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using NetCoreArchiveSystem.Data;
using NetCoreArchiveSystem.Models;
using System.IO;

namespace NetCoreArchiveSystem.Controllers
{
    public class ArchiveController : Controller
    {
        private readonly ArchiveDbContext _context;
        private readonly IWebHostEnvironment _environment;

        public ArchiveController(ArchiveDbContext context, IWebHostEnvironment environment)
        {
            _context = context;
            _environment = environment;
        }

        // GET: Archive (Ana Sayfa)
        public async Task<IActionResult> Index(string grup = "")
        {
            var query = _context.Klasorler.AsQueryable();
            if (!string.IsNullOrEmpty(grup))
            {
                query = query.Where(k => k.Grup == grup);
            }

            var klasorler = await query.ToListAsync();
            var evraklar = await _context.Evraklar.ToListAsync();

            // Calculate progress for each folder
            var klasorDurumlari = new List<dynamic>();

            foreach (var k in klasorler)
            {
                var kEvraklar = evraklar.Where(e => e.KlasorId == k.Id).Select(e => e.EvrakTipi).ToList();
                var zorunluList = string.IsNullOrEmpty(k.ZorunluEvraklar) ? new List<string>() : k.ZorunluEvraklar.Split(',').Select(x => x.Trim()).ToList();
                
                var eksikList = zorunluList.Where(z => !kEvraklar.Contains(z)).ToList();
                
                int yuzde = 100;
                if (zorunluList.Count > 0)
                {
                    yuzde = (int)(((zorunluList.Count - eksikList.Count) / (float)zorunluList.Count) * 100);
                }

                klasorDurumlari.Add(new
                {
                    Klasor = k,
                    EksikEvraklar = eksikList,
                    Yuzde = yuzde,
                    EksikSayisi = eksikList.Count,
                    ZorunluSayisi = zorunluList.Count
                });
            }

            ViewBag.SeciliGrup = grup;
            return View(klasorDurumlari);
        }

        // GET: Archive/Details/{id}
        public async Task<IActionResult> Details(string id)
        {
            if (id == null) return NotFound();

            var klasor = await _context.Klasorler.FindAsync(id);
            if (klasor == null) return NotFound();

            var evraklar = await _context.Evraklar.Where(e => e.KlasorId == id).ToListAsync();
            
            var zorunluList = string.IsNullOrEmpty(klasor.ZorunluEvraklar) ? new List<string>() : klasor.ZorunluEvraklar.Split(',').Select(x => x.Trim()).ToList();
            var yuklenenTipler = evraklar.Select(e => e.EvrakTipi).ToList();
            var eksikList = zorunluList.Where(z => !yuklenenTipler.Contains(z)).ToList();

            ViewBag.ZorunluList = zorunluList;
            ViewBag.EksikList = eksikList;
            ViewBag.Evraklar = evraklar;

            return View(klasor);
        }

        // POST: Archive/Upload
        [HttpPost]
        public async Task<IActionResult> Upload(string klasorId, string evrakTipi, IFormFile dosya)
        {
            if (string.IsNullOrEmpty(klasorId) || string.IsNullOrEmpty(evrakTipi) || dosya == null || dosya.Length == 0)
            {
                TempData["Error"] = "Lütfen tüm alanları doldurun ve bir dosya seçin.";
                return RedirectToAction(nameof(Details), new { id = klasorId });
            }

            // Create uploads directory if not exists
            var uploadsFolder = Path.Combine(_environment.WebRootPath, "uploads");
            if (!Directory.Exists(uploadsFolder))
            {
                Directory.CreateDirectory(uploadsFolder);
            }

            // Generate unique filename to avoid overwrites
            var uniqueFileName = Guid.NewGuid().ToString() + "_" + dosya.FileName;
            var filePath = Path.Combine(uploadsFolder, uniqueFileName);

            using (var stream = new FileStream(filePath, FileMode.Create))
            {
                await dosya.CopyToAsync(stream);
            }

            // Add to database
            var yeniEvrak = new Evrak
            {
                KlasorId = klasorId,
                EvrakTipi = evrakTipi,
                DosyaAdi = uniqueFileName,
                YuklemeTarihi = DateTime.Now
            };

            _context.Evraklar.Add(yeniEvrak);
            await _context.SaveChangesAsync();

            TempData["Success"] = "Dosya başarıyla yüklendi.";
            return RedirectToAction(nameof(Details), new { id = klasorId });
        }

        // POST: Archive/Delete/{id}
        [HttpPost]
        public async Task<IActionResult> Delete(int id, string klasorId)
        {
            var evrak = await _context.Evraklar.FindAsync(id);
            if (evrak != null)
            {
                // Delete physical file
                var filePath = Path.Combine(_environment.WebRootPath, "uploads", evrak.DosyaAdi);
                if (System.IO.File.Exists(filePath))
                {
                    System.IO.File.Delete(filePath);
                }

                // Delete from DB
                _context.Evraklar.Remove(evrak);
                await _context.SaveChangesAsync();
                
                TempData["Success"] = "Dosya başarıyla silindi.";
            }

            return RedirectToAction(nameof(Details), new { id = klasorId });
        }
    }
}
