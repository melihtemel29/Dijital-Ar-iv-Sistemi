using Microsoft.EntityFrameworkCore;
using NetCoreArchiveSystem.Models;
using System.Collections.Generic;

namespace NetCoreArchiveSystem.Data
{
    public class ArchiveDbContext : DbContext
    {
        public ArchiveDbContext(DbContextOptions<ArchiveDbContext> options)
            : base(options)
        {
        }

        public DbSet<Klasor> Klasorler { get; set; }
        public DbSet<Evrak> Evraklar { get; set; }

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            base.OnModelCreating(modelBuilder);

            // Seed initial data just like the python app
            modelBuilder.Entity<Klasor>().HasData(
                new Klasor { Id = "60-00", Ad = "60-00", Grup = "1. Bölüm", ZorunluEvraklar = "Şartname,Sözleşme,Fatura", BitisTarihiVarMi = true },
                new Klasor { Id = "60-01", Ad = "60-01", Grup = "1. Bölüm", ZorunluEvraklar = "Şartname,Fatura", BitisTarihiVarMi = false },
                new Klasor { Id = "61-00", Ad = "61-00", Grup = "2. Bölüm", ZorunluEvraklar = "Sözleşme,Ek Belge", BitisTarihiVarMi = true },
                new Klasor { Id = "62-00", Ad = "62-00", Grup = "3. Bölüm", ZorunluEvraklar = "Dilekçe,Rapor", BitisTarihiVarMi = false }
            );
        }
    }
}
